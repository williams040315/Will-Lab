Installation / start-up
----------------------------
1. Install the recommended version of Python and all of its OpenCV dependencies

Training 
--------
I carried out was done in two stages.
1. I validated the writing of the algorithm on eye images. In the training_eye file are the eye images (in images) and the corresponding masks (1st_manual). I launched the training algorithm by adjusting the loop for line 52 and the number of epochs line 109 to generate a prediction model in the models_generated file. It is not necessary to have a large dataset. You have to create new images from existing ones by adding noise, rotating, or changing the contrast, for example (traitement_images.py).
Once the model has been generated, simply load it and specify the file where the prediction images will be generated (prediction-10epochs-for4.py).

2. I started with the white light images of miss marple and with the use of the spot_detection (training-cell folder) as a mask. For now, I have only made 4 epochs with a partial result (result/missmarple-cell/miss-marple-4epochs-for6,7h folder).
You have to start training again with a more powerful machine because I am limited on mine (eg GPU). I can go up to 10 epochs after my CPU is saturated.

I will post the next results soon
------------------------------------------------------------------------------------------------------------------------------------------

Williams BRETT | Lab513 | wllmsbrtt@gmail.com for any questions
