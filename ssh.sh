#!/bin/bash

ssh -p $(python -c "from gadget_settings import MANHOLE_BIND_ADDRESS as addr; print addr.split(':')[1]") root@localhost
