#!/usr/bin/env python3

import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
        ["127.0.0.1"],
        http_auth=None, # http_auth=('user', 'secret')
        scheme="http",
        port=9200
        )

INDEX_PREFIX = "facebook-messenger"

MAPPING = json.loads("""

{
 "settings" : {
        "index" : {
            "number_of_shards" : 6,
            "number_of_replicas" : 0
        }
    },

"mappings" : {
      "properties" : {
        "content" : {
          "type" : "text"
        },
        "files" : {
          "properties" : {
            "creation_timestamp" : {
              "type" : "date",
              "format": "epoch_millis"
            },
            "uri" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "gifs" : {
          "properties" : {
            "uri" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "participants" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "photos" : {
          "properties" : {
            "creation_timestamp" : {
              "type" : "date",
              "format": "epoch_millis"
            },
            "uri" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "reactions" : {
          "properties" : {
            "actor" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "reaction" : {
                  "type" : "keyword",
                  "ignore_above" : 256
            }
          }
        },
        "sender_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "share" : {
          "properties" : {
            "link" : {
                  "type" : "keyword",
                  "ignore_above" : 256
            }
          }
        },
        "sticker" : {
          "properties" : {
            "uri" : {
                  "type" : "keyword",
                  "ignore_above" : 256
            }
          }
        },
        "timestamp_ms" : {
              "type" : "date",
              "format": "epoch_millis"
        },
        "type" : {
              "type" : "keyword",
              "ignore_above" : 256
        }
      }
    }
     }
""")
