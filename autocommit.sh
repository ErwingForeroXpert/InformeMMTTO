#!/bin/sh
d:
cd D:/Work/InformeMMTTO
git add --all
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
git commit -am "Regular auto-commit $(timestamp)"
git push origin develop:develop-backup