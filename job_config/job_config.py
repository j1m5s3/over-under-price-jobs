from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class Param:
    """Param for the job"""
    btc: List
    eth: List


@dataclass
class JobParams:
    """Params for the job"""
    params: Param


class JobConfig:
    def __init__(self, class_handler, job_name: str, job_params: JobParams):
        self.class_handler = class_handler
        self.job_name = job_name
        self.job_params = job_params
