# Setup
The following instructions are for getting started with our Capitol Gains Project.

## Step 0 - Prerequisites
Make sure you have the following:
- A current UW-Madison account through CSLabs.
- Docker Desktop installed on your computer.

## Step 1 - Docker Desktop 
Make sure Docker Desktop has been started and is running during your session.

<img src="docker-logo-blue.png" alt="Docker"  height="60" /> 

## Step 2 - Getting Started Locally / Remote
If you would like to run the project locally, first copy our project into a local repository.

Create a new folder you would like to store the project
```bash
git mkdir "CapitolGains"
git cd CapitolGains
```
 Run this command in your terminal:

```bash
git clone [ssh / https of GitLab repo]
```
In the terminal and with docker running, run this command:
```bash
docker compose up --build
```

Note: If this is the first time setup, this will take a few minutes.


If you are trying to connect to the project remotely, use this command:

```bash
 ssh -L 4803:localhost:5173 [username]@cs506x11.cs.wisc.edu
 ```

## Step 3 - Permissons
You will need a *.env* file to be able to access the project, as we have a password for the database. 

Contact your local Capitol Gains Team Member for more info.

## Step 4 - Final 
Now open up the webpage in your preferred browser using the localhost at the specified port when the build is stable.

You should be all set to start tracking your favorite politicians and where all their money goes! 

**Cheers, and Happy Trading!**
-Capitol Gains Team