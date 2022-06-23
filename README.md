
## Build Docker image

```sh
docker build -t cfleu198/kaili_button . --no-cache

docker push cfleu198/kaili_button

docker image prune
```

```sh
<!-- docker run -d -p 5001:5001 --name kaili_button -e MACHINE=machine03 -it cfleu198/kaili_button -->
docker run -d -p 5001:5001 --name kaili_button -it cfleu198/kaili_button

docker stop kaili_button

docker rm kaili_button
```



## Query

### Query by datetime
```js
db.button.find({
    "epoch_start":{"$gte": ISODate("2022-06-11T01:00:36+08:00")}
})
```

### Query by equipement
```js
db.button.find({
    "machine":"machine03"
})
```

### Query by datetime and equipement
```js
db.button.find({
    $and:[
        {"machine":"machine03"},
        {"epoch_start":{"$gte": ISODate("2022-06-11T01:00:36+08:00")}}
        ]
    
})
```

### Group by Product and Calculate SUM of PCS
```js
db.button.aggregate([ { 
    $group: { 
        _id: "$product", 
        sum: { $sum: "$pcs" }
    } 
} ] )
```

### Group by Product in a specific Datatime, and Calculas SUM of PCS
```js
db.button.aggregate([ 
    { 
        $match : {"epoch_start":{"$gte": ISODate("2022-06-15T01:00:36+08:00")}}
    },
    { 
        $group: { 
            _id: "$product", 
            sum: { $sum: "$pcs" }
        }
    } 
])
```

### Group by Machine in a specific Datatime, and Calculas SUM of PCS
```js
db.button.aggregate([ 
    { 
        $match : {"epoch_start":{"$gte": ISODate("2022-06-20T01:00:36+08:00")}}
    },
    { 
        $group: { 
            _id: "$machine", 
            sum: { $sum: "$pcs" }
        }
    } 
])
```