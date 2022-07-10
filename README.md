# Akamai Origin Server
```
https://1.2.3.4

http GET http://1.2.3.4/todo/api/list/tasks -v
http HEAD  http://1.2.3.4/todo/api/list/tasks -v

http POST http://1.2.3.4/todo/api/create/task -v <<< '{"title":"Reading","description":"Read a Story Book","done":false}'
http POST http://1.2.3.4/todo/api/create/task -v <<< '{"title":"Playing","description":"Play Football","done":false}'

http PUT http://1.2.3.4/todo/api/update/task/3 -v <<< '{"title":"Reading","description":"Read a Story Book","done":true}'

http OPTIONS http://1.2.3.4/todo/api/list/methods -v

http DELETE http://1.2.3.4/todo/api/delete/tasks/3 -v


Response Codes:
http POST http://1.2.3.4/todo/api/create/task -v <<< '{"title":"Reading,"description":"Read a Story Book","done":"False"}'

http POST http://1.2.3.4/todo/api/create/task -v <<< '{"title":"Reading","description":"Read a Story Book","done":"False"}'

http POST http://127.0.0.1/datastream -v <<< '{"title":"Reading","description":"Read a Story Book","done":false}'

http POST http://127.0.0.1/cloudmonitor -v <<< '{"title":"Reading","description":"Read a Story Book","done":false}'

```
