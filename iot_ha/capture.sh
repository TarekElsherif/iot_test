sudo fswebcam --no-banner -S 10 captured/test.jpg
sudo convert test.jpg -gravity center -crop 92x112+0+0 test_faces/face.jpg
