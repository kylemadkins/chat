import os

import grpc

import profanity_pb2
import profanity_pb2_grpc

PROFANITY_HOST = os.environ["PROFANITY_HOST"]


class ProfanityFilter:
    def censor(self, input):
        with grpc.insecure_channel(f"{PROFANITY_HOST}:50051") as channel:
            client = profanity_pb2_grpc.ProfanityStub(channel)
            request = profanity_pb2.ProfanityRequest(input=input)
            response = client.Filter(request)
            return response.censored
