================
WebRTC Streaming
================


.. image:: https://img.shields.io/pypi/v/webrtc-streaming.svg
        :target: https://pypi.python.org/pypi/webrtc-streaming

.. image:: https://api.travis-ci.com/Utring/webrtc_streaming.svg
        :target: https://travis-ci.com/Utring/webrtc_streaming

.. image:: https://readthedocs.org/projects/webrtc-streaming/badge/?version=latest
        :target: https://webrtc-streaming.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Utring/webrtc_streaming/shield.svg
     :target: https://pyup.io/repos/github/Utring/webrtc_streaming/
     :alt: Updates

.. image:: https://pepy.tech/badge/webrtc-streaming/month
        :target: https://pepy.tech/project/webrtc-streaming
        :alt: Documentation Status


Ready to use WebRTC Streaming


* Free software: BSD license
* Documentation: https://webrtc-streaming.readthedocs.io.



Dependencies
------------

OpenCV
~~~~~~

.. code:: bash

    # Remove previous OpenCV
    $ sudo apt-get purge libopencv*
    
    # Create and activate virtual environment
    $ ENV_NAME=dji_asdk_to_python_env
    $ cd $HOME && mkdir -p .virtualenvs && cd .virtualenvs
    $ virtualenv $ENV_NAME --python=python3.8
    $ source $ENV_NAME/bin/activate
    $ pip install numpy==1.20.1

    # Build OpenCV (with activated virtual environment)
    $ cd $HOME
    $ git clone https://github.com/opencv/opencv_contrib.git
    $ cd opencv && git checkout tags/4.5.1 && cd ..

    $ git clone https://github.com/opencv/opencv.git
    $ cd opencv && git checkout tags/4.5.1 && mkdir build && cd build

    $ cmake -D WITH_CUDA=ON \
            -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
            -D PYTHON_EXECUTABLE=/home/$USER/.virtualenvs/$ENV_NAME/bin/python \
            -D WITH_GSTREAMER=ON \
            -D WITH_LIBV4L=ON \
            -D BUILD_opencv_python2=OFF \
            -D BUILD_opencv_python3=ON \
            -D BUILD_TESTS=OFF \
            -D BUILD_PERF_TESTS=OFF \
            -D BUILD_EXAMPLES=OFF \
            -D CMAKE_BUILD_TYPE=RELEASE \
            -D CMAKE_INSTALL_PREFIX=/usr/local ..
    $ make -j4 # use 4 CPU cores
    $ sudo make install
    $ sudo ldconfig

    # Make sure python path exists
    $ cd ~/.virtualenvs/$ENV_NAME/lib/python3.6/site-packages
    $ ln -s /usr/local/lib/python3.8/site-packages/cv2/python-3.8/cv2.cpython-38-aarch64-linux-gnu.so cv2.so
    
    # Check OpenCV install
    $ python -c "import cv2; print(cv2.getBuildInformation());" | grep GStreamer


FFmpeg
~~~~~~

.. code:: bash

    $ wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/ffmpeg/7:4.2.4-1ubuntu0.1/ffmpeg_4.2.4.orig.tar.xz
    $ tar -xf ffmpeg_4.2.4.orig.tar.xz
    $ ./configure --disable-static --enable-shared --disable-doc
    $ make
    $ sudo make install
    $ sudo ldconfig


Features
--------

* Receive OpenCV images and send it using WebRTC


Install PyPI
------------

.. code:: bash

    $ pip install webrtc_streaming


Usage example
-------------
Check examples folder


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
