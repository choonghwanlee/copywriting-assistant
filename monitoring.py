import time
import boto3
from fastapi import Request
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')

# Create a middleware class for monitoring
class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Record start time
        start_time = time.time()
        
        # Get the route path
        route = request.url.path
        method = request.method
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Send metrics to CloudWatch
            cloudwatch.put_metric_data(
                Namespace='FastAPI/Production',
                MetricData=[
                    {
                        'MetricName': 'Latency',
                        'Value': duration * 1000,  # Convert to milliseconds
                        'Unit': 'Milliseconds',
                        'Dimensions': [
                            {'Name': 'Route', 'Value': route},
                            {'Name': 'Method', 'Value': method}
                        ]
                    },
                    {
                        'MetricName': 'Requests',
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {'Name': 'Route', 'Value': route},
                            {'Name': 'Method', 'Value': method}
                        ]
                    }
                ]
            )
            
            return response
            
        except Exception as e:
            # Record error metrics
            cloudwatch.put_metric_data(
                Namespace='FastAPI/Production',
                MetricData=[
                    {
                        'MetricName': 'Errors',
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {'Name': 'Route', 'Value': route},
                            {'Name': 'Method', 'Value': method},
                            {'Name': 'ErrorType', 'Value': type(e).__name__}
                        ]
                    }
                ]
            )
            raise