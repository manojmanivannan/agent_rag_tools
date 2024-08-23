FROM neo4j:community

RUN apt install --quiet procps

COPY create-graph.sh create-graph.sh
COPY wrapper.sh wrapper.sh
COPY subset-create-meta-nodes.cypher .
COPY subset-create-review-nodes-split-00.cypher .
COPY subset-create-review-nodes-split-01.cypher .
COPY subset-create-review-nodes-split-02.cypher .
COPY subset-create-review-nodes-split-03.cypher .
COPY subset-create-review-nodes-split-04.cypher .
COPY subset-create-review-nodes-split-05.cypher .
COPY subset-create-index.cypher .

RUN chmod +x ./wrapper.sh ./create-graph.sh

ENTRYPOINT [ "./wrapper.sh" ]