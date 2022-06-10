
# Build Docker image

docker build -t cfleu198/kaili_button . --no-cache

<!-- docker run -d -p 5001:5001 --name kaili_button -e MACHINE=machine03 -it cfleu198/kaili_button -->
docker run -d -p 5001:5001 --name kaili_button -it cfleu198/kaili_button

docker push cfleu198/kaili_button

docker stop kaili_button

docker rm kaili_button

docker image prune