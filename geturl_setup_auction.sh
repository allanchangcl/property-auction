#!/bin/bash
python3 auction_geturl_table_setup.py &&
python3 auction_geturl_kl.py &&
python3 auction_geturl_pe.py &&
python3 auction_geturl_pk.py &&
python3 auction_geturl_se.py &&
python3 auction_newurl_table_setup.py &&
python3 auction_expiry.py