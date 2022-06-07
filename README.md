
# Build Docker image

docker build -t cfleu198/kaili_button . --no-cache

docker run -d -p 5001:5001 --name kaili_button -it cfleu198/kaili_button

docker push cfleu198/kaili_button