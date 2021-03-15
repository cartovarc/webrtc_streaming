import cv2
import socketio
import asyncio
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc import VideoStreamTrack
from av import VideoFrame


async def _start_streaming(video_capture=None,
                           img_size=None,
                           secret_key=None,
                           signaling_server=None,
                           path=None):

    class CV2Track(VideoStreamTrack):
        """
        A video stream that returns an cv2 track
        """

        def __init__(self):
            super().__init__()  # don't forget this!
            self.img = np.random.randint(
                255, size=(720, 1280, 3), dtype=np.uint8)

        async def recv(self):
            pts, time_base = await self.next_timestamp()
            ret, new_img = video_capture.read()
            if ret is True and new_img is not None:
                self.img = new_img
            if img_size is not None:
                self.img = cv2.resize(self.img, img_size,
                                      interpolation=cv2.INTER_AREA)
            frame = VideoFrame.from_ndarray(self.img, format="bgr24")
            frame.pts = pts
            frame.time_base = time_base
            return frame

    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print("Connected to server %s" % signaling_server)
        await sio.emit("create_room", secret_key)

    @sio.event
    async def viewer_need_offer(data):
        pcs = set()

        viewer_id = data["viewer_id"]
        print("Server ask for offer to viewer " + viewer_id)

        remote_description = data["offer"]
        sdp = remote_description["sdp"]
        type_ = remote_description["type"]

        offer = RTCSessionDescription(sdp=sdp, type=type_)
        pc = RTCPeerConnection()
        pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        cv2_track = CV2Track()

        await pc.setRemoteDescription(offer)

        for t in pc.getTransceivers():
            if t.kind == "video":
                pc.addTrack(cv2_track)
                print("cv2_tracker added...")

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        offer = {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }
        await sio.emit("offer_to_viewer",
                       {"viewer_id": viewer_id, "offer": offer})

    @sio.event
    def disconnect():
        print('Disconnected from server')

    await sio.connect(signaling_server, socketio_path=path)
    await sio.wait()


def start_streaming(video_capture=None,
                    img_size=None,
                    secret_key=None,
                    signaling_server=None,
                    path=None):
    assert video_capture is not None
    assert secret_key is not None
    assert signaling_server is not None
    assert path is not None

    loop = asyncio.get_event_loop()
    coro = asyncio.run(_start_streaming(
        video_capture=video_capture,
        img_size=img_size,
        secret_key=secret_key,
        signaling_server=signaling_server,
        path=path))

    if loop.is_running():
        asyncio.run(coro)
    else:
        loop.run_until_complete(coro)
