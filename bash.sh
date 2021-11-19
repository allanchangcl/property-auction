
# copy database from htpc
scp allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite /home/allanchangcl/webdev/pythona/myproperty

scp allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty/sale.sqlite /home/allanchangcl/webdev/pythona/myproperty

# copy db back to htpc
scp /home/allanchangcl/webdev/pythona/myproperty/sale.sqlite allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty

# copy scripy to htpc
scp /home/allanchangcl/webdev/pythona/myproperty/auction.py allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty

scp /home/allanchangcl/webdev/pythona/myproperty/auction_geturl_kl.py allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty

scp /home/allanchangcl/webdev/pythona/myproperty/sale_kl.py allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty

scp /home/allanchangcl/webdev/pythona/myproperty/sale.py allanchangcl@192.168.1.110:/home/allanchangcl/Webdev/Pythona/Myproperty