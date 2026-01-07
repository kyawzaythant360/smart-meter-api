curl -X POST http://localhost:8000/register \
 -H "Content-Type: application/json" \
 -d '{
"name": "facilitator1",
"password": "password123"
}'

curl -X POST http://localhost:8000/login \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=facilitator1" \
 -d "password=password123" \
 -d "grant_type=password"

curl -X POST http://localhost:8000/login \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=facilitator1" \
 -d "password=password123" \
 -d "grant_type=password"

curl -X POST http://localhost:8000/usage \
 -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
 -H "Content-Type: application/json" \
 -d '{
"kilowatts_used": 12.5
}'

curl -X POST http://localhost:8000/refresh \
 -H "Content-Type: application/json" \
 -d '{
"refresh_token": "REFRESH_TOKEN_HERE"
}'

curl -X GET http://localhost:8000/usage \
 -H "Authorization: Bearer NEW_ACCESS_TOKEN"

curl -X POST http://localhost:8000/refresh \
 -H "Content-Type: application/json" \
 -d '{
"refresh_token": "INVALID_TOKEN"
}'

curl -X POST http://localhost:8000/refresh \
 -H "Content-Type: application/json" \
 -d '{
"refresh_token": "OLD_REFRESH_TOKEN"
}'
