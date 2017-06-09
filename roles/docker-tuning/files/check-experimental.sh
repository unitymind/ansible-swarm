#!/bin/bash

docker version -f '{{.Server.Experimental}}'
