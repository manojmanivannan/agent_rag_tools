DROP INDEX product_index IF EXISTS;
CREATE VECTOR INDEX `product_index` IF NOT EXISTS FOR (p:Product) ON (p.textEmbedding) OPTIONS { indexConfig: {`vector.dimensions`: 384, `vector.similarity_function`: 'cosine'}};
