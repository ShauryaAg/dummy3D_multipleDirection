# Human Mimic
Its a project to try to make a 3D model mimic human actions by only using minimal hardware, that is, two phone cameras and clicking a pair of stereo images.

## Our approach
Already existing models like OpenPose and Posenet already offer the ability to get the 2D coordinates of certain points of our body, but they lack in 3D coordinates.
For our purpose we used OpenPose to get the 2D coordinates.

We created a depth map of the image using the two stereo images clicked using the two cameras, and tried to estimate the depth of each point using the depth map.

Once the 2D coordinates are attained and depth map is created, we convert those points into 3D by adding a Z-coordinate using the depth map.
Since there might variations in different scenarios, the Z-coordinates we make are respective to a certain point on our body (the center of our chest).

The depth map created using a pair of stereo images looks like this:
![depth_map_image_bike](https://user-images.githubusercontent.com/31778302/69337940-1d025880-0c88-11ea-84da-960c43f90b9e.png)

Then using the 3D coordinates, the 3D model is animated by calculating the angles between each bone with every axis and rotating the respective bone accordingly.


## Future Scope
We wish to use this model to help train athletes better, by highlighting the muscle that might get hurt during a certain pose and hence showing the correct posture.

Moreover, this can be used in game development as the game studios might be able to skip the high costs of motion capture suits (if we are able to achieve that level of accuracy).
