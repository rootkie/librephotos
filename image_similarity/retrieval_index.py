import datetime
import json

import faiss
import numpy as np
from utils import logger

embedding_size = 512


class RetrievalIndex(object):
    def __init__(self):
        pass
        self.indices = {}
        self.image_hashes = {}

    def build_index_for_user(self, user_id, image_hashes, image_embeddings):
        logger.info(
            "building index for user {} - got {} photos to process".format(
                user_id, len(image_hashes)
            )
        )
        start = datetime.datetime.now()
        self.indices[user_id] = faiss.IndexFlatIP(embedding_size)
        self.image_hashes[user_id] = []

        for h, e in zip(image_hashes, image_embeddings):
            self.image_hashes[user_id].append(h)
            self.indices[user_id].add(np.array([e], dtype=np.float32))

        elapsed = (datetime.datetime.now() - start).total_seconds()
        logger.info(
            "finished building index for user %d - took %.2f seconds"
            % (user_id, elapsed)
        )

    def search_similar(self, user_id, in_embedding, n=100, thres=27.0):
        dist, res_indices = self.indices[user_id].search(
            np.array([in_embedding], dtype=np.float32), n
        )

        res = []
        for distance, idx in zip(dist[0], res_indices[0]):
            if distance >= thres:
                res.append(self.image_hashes[user_id][idx])
        logger.info("searched {} images for user {}".format(n, user_id))
        return res
