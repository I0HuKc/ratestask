# API launch

***Docker must be installed on the computer.***

1. Clone the repo;
2. Build docker compose file;
3. Up docker compose file;


## Using
* Host: 127.0.0.1
* Port: 5000

Required query parameters

* date_from
* date_to
* origin
* destination

Request example

```
http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main
```

Response example

```
[
  {
    "average_price": "1371",
    "day": "2016-01-01"
  },
  {
    "average_price": "808",
    "day": "2016-01-01"
  },
  {
    "average_price": "882",
    "day": "2016-01-01"
  },
  {
    "average_price": "936",
    "day": "2016-01-01"
  },
  {
    "average_price": "1139",
    "day": "2016-01-01"
  },
  {
    "average_price": "1324",
    "day": "2016-01-01"
  },
    ...
]
```

## Difficulties and problems I faced

### Architectural dilemma. 

Compact and simple or scalable and bulky... The service is required to contain only 1 API endpoint. On the one hand, something super complex in terms of architecture is not required here, even just one file is enough. On the other hand, although this is a test project, we should always consider possible scaling. Therefore, I decided to use a deliberately scalable architecture, but with minimal functionality, so that the project does not look too cumbersome and does not have deep file nesting.

### The rule of project completion dates (90 to 90)

> The first 90% of work takes 10% of the time, 
> and the last 10% - the remaining 90% of the time.

I implemented almost the entire task with one SQL request, so there were no difficulties with writing python code at all, like most of the SQL request. 
I ran into difficulties at the end with a banal ORDER BY. I was trying to solve the problem of excluding duplicates from the resulting dataset. Initially, I thought that this should be implemented by using a DISTINCT predicate. But then I realized that I do not need to remove them, but simply merge them.

### Other
* OS: Linux(Ubuntu)
* Python: 3.10
* Elapsed time: ~4-5h
