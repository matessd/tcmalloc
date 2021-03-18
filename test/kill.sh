#!/bin/bash
pid=$(pgrep $1)
kill -9 $pid
