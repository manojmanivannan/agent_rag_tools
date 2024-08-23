#!/bin/bash

sleep 5

USERNAME=$( echo $NEO4J_AUTH | cut -d '/' -f 1)
PASSWORD=$( echo $NEO4J_AUTH | cut -d '/' -f 2)

FIRST_LINE=$(head -n1 subset-create-meta-nodes.cypher)
echo "Creating nodes from create-meta-nodes.cypher"

until  echo $FIRST_LINE | cypher-shell -u $USERNAME -p $PASSWORD
do
  echo "create meta nodes failed, sleeping 5 seconds"
  sleep 5
done


run_command_line_by_line(){
  local input_file=$1
  while IFS= read -r line
  do
    echo $line
    echo "$line" | cypher-shell -u $USERNAME -p $PASSWORD || true
  done < "$input_file"
}

echo "Running  subset-create-review-nodes.cypher"
cypher-shell -f subset-create-review-nodes-split-00.cypher -u $USERNAME -p $PASSWORD
cypher-shell -f subset-create-review-nodes-split-01.cypher -u $USERNAME -p $PASSWORD
cypher-shell -f subset-create-review-nodes-split-02.cypher -u $USERNAME -p $PASSWORD
cypher-shell -f subset-create-review-nodes-split-03.cypher -u $USERNAME -p $PASSWORD
cypher-shell -f subset-create-review-nodes-split-04.cypher -u $USERNAME -p $PASSWORD
cypher-shell -f subset-create-review-nodes-split-05.cypher -u $USERNAME -p $PASSWORD

echo "Running  subset-create-meta-nodes.cypher nodes"
cypher-shell -f subset-create-meta-nodes.cypher -u $USERNAME -p $PASSWORD
# run_command_line_by_line subset-create-meta-nodes.cypher

echo "Running subset-create-index.cypher"
cypher-shell -f subset-create-index.cypher -u $USERNAME -p $PASSWORD


echo "Graph creation complete"