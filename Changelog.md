# ThreeDRendering Changelog
This project started on 25/10/21.  
Versions 1 to 3 were created before I uploaded this to GitHub, as a result they can't be found in previous versions.  
- I thought I would leave them here so at least the thoughts behind things is still documented.

## Version 1
Created file for vector and plane math.  
Cuboids are simple 3D objects to start with.  
Camera to render the cuboid.

### Created "Vectors_and_Planes.py" and the Vector, Ray and Plane classes.  
Designed to assist with any calculations.  
Added 3 test cases for the major use functions:  
- Dot.
- Dot Product.
- Cross Product.
- Ray Intersection With Plane.

These tests can be individually toggled.  

### Created Cuboid class
Just a store of information about a cuboid.
- The coordinates of the bottom, front left of the cuboid.
- The width, height and length.
- The normals for each face.
- Plane definitions for the faces.
- The coordinates of each corner.
- Which corners connect.
- Which corner connections belong to which faces.
- Anything else I may have forgotten about whilst writing this, looking at the class will be the best way to see things.

Definitions for the above things can be found in the Images folder.  

### Created Camera class
Contains information used to render things, such as the view plane and position.  
The camera can be moved left and right.  
Has a function called "render_cuboid".  
- I don't really know what this does.

As of right now only the cuboid can be rendered, other things will be added later.  
- Maybe.

### Created "main.py"
Contains the Cuboid and Camera class.  
These classes have been used to display what should be a cube.  
- It looks like a rectangular prism, but ehh, I have a 3D thing being displayed, and I can move the camera.

The camera can be moved to the left and right using the 'a' and 'd' keys.  

### Ideas of things to add or improve
- Move camera movement.
  - Vertical movement.
  - Moving forward and back.

### Bugs and things to fix
- What should be a cube isn't rendered with equal width and height.
  - Hence, it isn't a cube.
  - This is probably due to the field of view being incorrectly calculated.
- Movement of the camera to the left and right causes the cuboid to be rendered incorrectly.
  - I realised this after waving a box around my face like a maniac.
  - Good luck fixing future me.

## Version 2
Adding more movement to the camera.  
Trying to make this into a package.  

### Renamed "Vectors_and_Planes.py" to "Vector_Math.py"
I feel this is a more fitting name.  

### Package, kind of, maybe
Attempting to throw everything into a package called "ThreeDRenderer".  
- I can't figure out why I called it that.

Should allow for better organising of the code and easier development.  
Maybe easier use, I don't really know.  
Moved a bunch of the code around as a result:  
- Camera class moved into its own file.
  - "render_cuboid" was moved out of this class and into a new file called "renderer.py".
    - The camera is passed as a parameter.
- Cuboid class moved into its own file.
  - Did you know that Camera and Cuboid have the same number of letters, making this look nice in a monospaced font?
- "Vector_Math.py" also moved into the package.

### Camera improvement
- Camera can now be moved up and down AND forward and back.
  - Cool right?
- Fixed the fov being calculated incorrectly.
  - I think.
- Not much else...

### Ideas of things to add or improve
- Camera rotation would be nice.
- Maybe also zooming in/out.

### Bugs and things to fix
- Still the cube isn't being rendered correctly when the camera is moving.

## Version 3
Fixing the rendering problem.  
Moving some stuff around.  
General improvements to "Vector_Math.py".  

### Moved some stuff around
- "renderer.py" removed
- "render_cuboid" is renamed to "cuboid" and moved into a new folder "renderer"

### Camera changes
Found out the problem with the incorrect rendering when moving the camera.  
I was moving the view point, but never adjusted where the plane was being rendered.  
So think of it like looking through a window, what you see is what is rendered.  
You were moving, but the window wasn't being moved with you.

### Adjustments to "Vector_Math.py"
For the Vector class:  
- Created some alternate constructors.
- Implemented some dunder methods, divide, equals and multiply.

For the Plane class:  
- The function "get_shortest_distance_to_point" was added.

Functions:  
- The function "get_vector_from_to" was added.
- The function "get_vector_from_yaw_pitch" was added.
  - This function currently doesn't work as intended, as such it shouldn't be used.

Other:
- General improvements to the functions in the Vector class to make them run faster.
  - Mainly replacing any use of loops with stuff just hard coded in.

### Added "Frustum.py"'
Originally to add in frustum culling, but I am getting a bit ahead of myself.  
Very unfinished, but I don't want to delete it, so it shall remain here.  

### Ideas of things to add or improve
- Camera rotation still would be nice.
  - Maybe just left and right rotation for now.
- Fov, so it works with differing values other than 60 degrees.

### Bugs and things to fix
- As of right now there are none.
  - Amazing
  
## Version 4
Found and fixed problems regarding the fov.

### Camera changes
Realised the fov was still being calculated incorrectly.  
- The problem was the way I was going about it, I think.
- I was considering sine and cosine to be linear functions (hint, they aren't).
- So I removed the y fov calculations, leaving the x fov ones.
- I then used the ratio to calculate the y limit from the x limit.
  - This seems to work nicely.

I guess I lied in the previous version about there being no bugs.  

Removed the old camera and replaced it with Camera2, now named Camera.  
- The new camera now has some functions to adjust the fov.
  - The fov is clamped between pi/100 and 99/100 pi to prevent interesting, but incorrect, things from happening.
  - As of now only x fov can be used, I may do y fov later.

### "main.py" changes
- Extra information is now displayed in the pygame window.
- The scroll wheel is used to change the fov.

### Ideas of things to add or improve
- Camera rotation please future me.

### Bugs and things to fix
- There shouldn't be any.
  - I think.

## Version 5
Words.  

### Things
Words.  
