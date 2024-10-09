# Research Report

## Intro to Docker and implementation of docker and docker compose

### Summary of Work

I researched on what docker and how to implement for our project, particularly the frontend of the project since I was resposible for implementing that. I learned about docker and docker compose and implementing them.

### Motivation

Our project is using a frontend in javascript using reach and vite and the backend is being implemented in python and Django. To host the all the parts in a container so that they can be used by anyone in the world with a laptop or a computer it was essential that we hosted containerised the project and and for that we needed to use docker. We needed docker compose to network the different docker containers that we are making for each part of the project i.e. API, web and backend. Without docker compose we would have to startup all the files in a network each time we wanted to run, compose file essentially automates that and hence the research.

### Time Spent

~30 minutes reading the documentations

~150 minutes following the video tutorial

~120 minutes implementing the Docker (pair programmed quite a bit of chunck) {Not a part of research}

### Results

I first saw two videos which were each 1 hour in length that whose link are given below. The first video introduced me to docker and dockerhub. Dockerhub is a place where anyone can host their docker containers and anyone can use it from there. It is also the place where many companies store their docker containers which we use in the project for example we have used node that was hosted there for the frontend.
The second video had overlap with the first video but gave me a better understanding of post binding which was essential for the project since we later ran into the problem since we got confused with the host between vite and react each of which use a different port. I learned the basic commands for docker in these videos. The videos also taught about tag and images which is very important to know. These videos also taught me about repositories and registries.
Using these two videos I successfully made the docker file for the frontend which did not take that much time since it was just couple of commands in the  Dockerfile, that is very easy to make in VS Code. There were some docker commands specific to docker that should be kept in mind. You can reference those from the docker file for web inside the frontend part.

After this I saw another 1 hour video on docker compose which introduced me to networks. First it showed me what I would do with dockor compose files and how that would take a lot of time it also showed me the difference between start, stop, up and down commands which is very important for keeping the data persistant. Then I followed the video and made a docker compose file. This part was very difficult and I had to go to the official docker hub documentation but I was still not able to solve a lot of it. Ultimately I had to pair program for this, even then I was not able to completely able to completely solve all the errors. The containerisation works in the VM but not in my PC for which I will talk with the TA and trouble shoot. The link to the video is also provided. I did not spend much time on the documentation but it is the official dockerhub documentation.

We also later set up a environment variables file on the computer to keep the passwords and everything hidden. Still working with this. There are not a lot of lines of code in the yml file for docker compose and it can easily be seen below the web tab which contains only the yml file.


### Sources

For the docker files
https://www.youtube.com/watch?v=pTFZFxd4hOI&ab_channel=ProgrammingwithMosh
https://www.youtube.com/watch?v=pg19Z8LL06w&ab_channel=TechWorldwithNana

for docker compose
https://www.youtube.com/watch?v=SXwC9fSwct8&ab_channel=TechWorldwithNana

additional resource
For docker containerisation of frontend in a small quick format with all the commands
https://www.youtube.com/watch?v=QePBbG5MoKk&ab_channel=NetNinja
