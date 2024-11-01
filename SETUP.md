# Setup for Capitol Gains App
This file explains how to get started with our project.

Make sure you have access to Docker Desktop
## Step 1 
Make sure Docker Desktop has been started and is running during your session.

TODO: ADD VISUAL FOR DOCKER DESKTOP

## Step 2
If you are running the project locally, then run this command in your terminal:

```bash
docker compose up --build
```

If you are trying to connect to the project remotely:
```bash
 ssh -L 4803:localhost:5173 [username]@cs506x11.cs.wisc.edu
 ```

## Step 3
Now open up the localhost in your browser at the specified port