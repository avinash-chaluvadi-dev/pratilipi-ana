""" [Configuration parameters for Topic classifier]

This module holds all the configuration parameters required for 
TOPIC_CLASSIFIER package

This file can also be imported as a module and contains the following 
below parameters
"""

import os

os.environ["CURL_CA_BUNDLE"] = ""

from datetime import datetime

from simpletransformers.language_representation import RepresentationModel
from transformers import logging

## Word/Sentence Embedding Parameters
CUDA = False  # CUDA parameter if set True uses GPU computation
logging.set_verbosity_error()  # Let's set the verbosity to error so that it discards printing warning messages on console

# Let's load the bert-embeddings model which is used to encode the sentences/words
model = RepresentationModel(
    model_type="bert", model_name="bert-base-uncased", use_cuda=CUDA
)


## Training Parameters
MESSAGE_COLUMN = "Message"  # Input column name in training data excel file
LABEL_COLUMN = "Reason for Call "  # Output column name in training data excel file
VOICE_MAIL_DATA = "voicemail_data.xlsx"  # Training file name


## S3 Bucket Parameters
BUCKET_NAME = "hive-s3-lz"  # Bucket name to load/save the artifacts
BASE_PREFIX = "medicare-voicemail"  # Base prefix of bucket
DATASET_PREFIX = f"{BASE_PREFIX}/dataset"  # Dataset prefix to load/save data files

# Let's create the model_name in datetime format
TOPIC_CLASSIFIER = datetime.now().strftime("Topic_Classifier_Model_%H-%M-%d-%m-%Y")

# Model prefix to load/save the model
MODEL_PREFIX = f"{BASE_PREFIX}/models/{TOPIC_CLASSIFIER}"

## Local File System Params

# Root directory of the topic_classifier project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
MODEL_DIR = ROOT_DIR + "/models"  # Model directory to load the model
MODEL_NAME = "svm.pkl"  # Name of the model to load from MODEL_DIR


# Output Labels
LABELS = [
    "Access to Care",
    "Authorization",
    "Benefits",
    "Claim",
    "EE Benefits",
    "Grievance and/or Appeal",
    "ID Card",
    "Membership/Enrollment",
    "Monthly Premium",
    "Need Case Management",
    "No Reason Given",
    "Nurse Line",
    "OTC",
    "Provider",
    "RX/Pharmacy",
    "Transportation",
]
