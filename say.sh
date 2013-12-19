#!/bin/bash

echo $@ | nc -uc localhost $(python -c "from gadget_settings import ECHOER_BIND_ADDRESS as addr; print addr.split(':')[1]")
