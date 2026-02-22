from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS for all origins (required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

DATA = [
    {"region": "apac", "lat": 130.36, "up": 98.128},
    {"region": "apac", "lat": 182.96, "up": 99.336},
    {"region": "apac", "lat": 128.52, "up": 99.054},
    {"region": "apac", "lat": 181.52, "up": 99.071},
    {"region": "apac", "lat": 191.3, "up": 98.743},
    {"region": "apac", "lat": 194.75, "up": 97.909},
    {"region": "apac", "lat": 223.67, "up": 99.148},
    {"region": "apac", "lat": 113.26, "up": 98.626},
    {"region": "apac", "lat": 124.88, "up": 99.104},
    {"region": "apac", "lat": 181.51, "up": 97.947},
    {"region": "apac", "lat": 206.96, "up": 99.23},
    {"region": "apac", "lat": 125.31, "up": 99.253},

    {"region": "emea", "lat": 114.61, "up": 98.156},
    {"region": "emea", "lat": 196.29, "up": 98.556},
    {"region": "emea", "lat": 180.94, "up": 97.374},
    {"region": "emea", "lat": 149.93, "up": 98.846},
    {"region": "emea", "lat": 201.44, "up": 97.684},
    {"region": "emea", "lat": 217.14, "up": 99.272},
    {"region": "emea", "lat": 168.61, "up": 97.949},
    {"region": "emea", "lat": 209.51, "up": 98.965},
    {"region": "emea", "lat": 191.26, "up": 97.525},
    {"region": "emea", "lat": 131.31, "up": 98.288},
    {"region": "emea", "lat": 217.69, "up": 97.657},
    {"region": "emea", "lat": 140.05, "up": 98.473},

    {"region": "amer", "lat": 195.01, "up": 99.119},
    {"region": "amer", "lat": 199.35, "up": 98.751},
    {"region": "amer", "lat": 206.78, "up": 97.261},
    {"region": "amer", "lat": 181.62, "up": 99.219},
    {"region": "amer", "lat": 137.31, "up": 98.112},
    {"region": "amer", "lat": 174.59, "up": 97.482},
    {"region": "amer", "lat": 199.25, "up": 99.193},
    {"region": "amer", "lat": 175.79, "up": 98.442},
    {"region": "amer", "lat": 202.95, "up": 99.441},
    {"region": "amer", "lat": 221.57, "up": 98.229},
    {"region": "amer", "lat": 191.79, "up": 99.406},
    {"region": "amer", "lat": 187.01, "up": 98.074},
]


@app.post("/")
async def metrics(body: dict):
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    response = {}

    for r in regions:
        reg_data = [x for x in DATA if x["region"] == r]
        if not reg_data:
            continue

        lats = [x["lat"] for x in reg_data]
        ups = [x["up"] for x in reg_data]

        response[r] = {
            "avg_latency": round(float(np.mean(lats)), 2),
            "p95_latency": round(float(np.percentile(lats, 95)), 2),
            "avg_uptime": round(float(np.mean(ups)), 3),
            "breaches": sum(1 for l in lats if l > threshold),
        }

    return response
# from http.server import BaseHTTPRequestHandler
# import json
# import numpy as np

# DATA = [
#     {"region": "apac", "lat": 130.36, "up": 98.128}, {"region": "apac", "lat": 182.96, "up": 99.336},
#     {"region": "apac", "lat": 128.52, "up": 99.054}, {"region": "apac", "lat": 181.52, "up": 99.071},
#     {"region": "apac", "lat": 191.3, "up": 98.743}, {"region": "apac", "lat": 194.75, "up": 97.909},
#     {"region": "apac", "lat": 223.67, "up": 99.148}, {"region": "apac", "lat": 113.26, "up": 98.626},
#     {"region": "apac", "lat": 124.88, "up": 99.104}, {"region": "apac", "lat": 181.51, "up": 97.947},
#     {"region": "apac", "lat": 206.96, "up": 99.23}, {"region": "apac", "lat": 125.31, "up": 99.253},
#     {"region": "emea", "lat": 114.61, "up": 98.156}, {"region": "emea", "lat": 196.29, "up": 98.556},
#     {"region": "emea", "lat": 180.94, "up": 97.374}, {"region": "emea", "lat": 149.93, "up": 98.846},
#     {"region": "emea", "lat": 201.44, "up": 97.684}, {"region": "emea", "lat": 217.14, "up": 99.272},
#     {"region": "emea", "lat": 168.61, "up": 97.949}, {"region": "emea", "lat": 209.51, "up": 98.965},
#     {"region": "emea", "lat": 191.26, "up": 97.525}, {"region": "emea", "lat": 131.31, "up": 98.288},
#     {"region": "emea", "lat": 217.69, "up": 97.657}, {"region": "emea", "lat": 140.05, "up": 98.473},
#     {"region": "amer", "lat": 195.01, "up": 99.119}, {"region": "amer", "lat": 199.35, "up": 98.751},
#     {"region": "amer", "lat": 206.78, "up": 97.261}, {"region": "amer", "lat": 181.62, "up": 99.219},
#     {"region": "amer", "lat": 137.31, "up": 98.112}, {"region": "amer", "lat": 174.59, "up": 97.482},
#     {"region": "amer", "lat": 199.25, "up": 99.193}, {"region": "amer", "lat": 175.79, "up": 98.442},
#     {"region": "amer", "lat": 202.95, "up": 99.441}, {"region": "amer", "lat": 221.57, "up": 98.229},
#     {"region": "amer", "lat": 191.79, "up": 99.406}, {"region": "amer", "lat": 187.01, "up": 98.074}
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"],
# )

# # 2. Catch-all for Errors (Ensures 401, 400, 413 have the header)
# @app.exception_handler(Exception)
# async def all_exception_handler(request: Request, exc: Exception):
#     status_code = exc.status_code if hasattr(exc, 'status_code') else 500
#     detail = exc.detail if hasattr(exc, 'detail') else str(exc)
#     return JSONResponse(
#         status_code=status_code,
#         content={"detail": detail},
#         headers={"Access-Control-Allow-Origin": "*"}
#     )
# class handler(BaseHTTPRequestHandler):
#     def do_OPTIONS(self):
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         self.send_header('Access-Control-Allow-Headers', 'Content-Type')
#         self.end_headers()

#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         body = json.loads(post_data)
        
#         req_regions = body.get("regions", [])
#         threshold = body.get("threshold_ms", 180)
        
#         response_data = {}
#         for r in req_regions:
#             reg_data = [x for x in DATA if x["region"] == r]
#             if not reg_data: continue
#             lats = [x["lat"] for x in reg_data]
#             uptimes = [x["up"] for x in reg_data]
            
#             response_data[r] = {
#                 "avg_latency": round(float(np.mean(lats)), 2),
#                 "p95_latency": round(float(np.percentile(lats, 95)), 2),
#                 "avg_uptime": round(float(np.mean(uptimes)), 3),
#                 "breaches": sum(1 for l in lats if l > threshold)
#             }

#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()
#         self.wfile.write(json.dumps(response_data).encode('utf-8'))
