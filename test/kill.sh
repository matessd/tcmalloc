#!/bin/bash
pid=$(pgrep tcmalloc)
kill -9 $pid
