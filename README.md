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


curl -X POST "http://localhost:8000/demo/populate" \
  -H "Content-Type: application/json" \
  -d '{"num_products": 2, "num_days": 5, "facilitator_name": "demo_facilitator"}'


curl -X POST "http://localhost:8000/products/6964c2c26cd17f91c538a49c/sim" \
  -H "Content-Type: application/json" \
  -d '{
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWNpbGl0YXRvcjEiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4MjY0MzE4fQ.GWv068Ajhk91gKN-RsvWW2AEa_z0Zv-mn7pYfnW-fmY",
        "product_id": "6964bf4daf5f95aeaff1b7be",
        "start": "2025-12-13T09:45:38.355+00:00",
        "end": "2025-12-13T09:45:38.355+00:00",
        "page": 1,
        "per_page": 5
      }'

curl -X GET "http://localhost:8000/products/6964bf4daf5f95aeaff1b7be
/sim?start=2025-12-21T09:54:40.535+00:00&end=2025-12-21T09:54:40.535+00:00&page=1&per_page=5"\-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWNpbGl0YXRvcjEiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4MjY0MzE4fQ.GWv068Ajhk91gKN-RsvWW2AEa_z0Zv-mn7pYfnW-fmY"


curl "http://localhost:8000/products/6964bf4daf5f95aeaff1b7be/sim?start=2025-12-13T09:45:38.355+00:00&end=2025-12-20T23:59:59+00:00&page=1&per_page=5" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWNpbGl0YXRvcjEiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4MjY0MzE4fQ.GWv068Ajhk91gKN-RsvWW2AEa_z0Zv-mn7pYfnW-fmY"


curl "http://localhost:8000/products/6964bf4daf5f95aeaff1b7be/sim?start=2025-12-13T09:45:38.355%2B00:00&end=2025-12-20T23:59:59.000%2B00:00&page=1&per_page=5" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWNpbGl0YXRvcjEiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4MjY0MzE4fQ.GWv068Ajhk91gKN-RsvWW2AEa_z0Zv-mn7pYfnW-fmY"
