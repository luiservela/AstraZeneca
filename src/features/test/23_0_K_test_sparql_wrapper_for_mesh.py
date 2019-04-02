from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://id.nlm.nih.gov/mesh/sparql")
#sparql.setQuery("""
#                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#                PREFIX owl: <http://www.w3.org/2002/07/owl#>
#                PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
#                PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
#                PREFIX mesh2015: <http://id.nlm.nih.gov/mesh/2015/>
#                PREFIX mesh2016: <http://id.nlm.nih.gov/mesh/2016/>
#                PREFIX mesh2017: <http://id.nlm.nih.gov/mesh/2017/>
#
#                SELECT ?treeNum ?ancestorTreeNum ?ancestor ?alabel
#                FROM <http://id.nlm.nih.gov/mesh>
#
#                WHERE {
#                    mesh:D008545 meshv:treeNumber ?treeNum .
#                    ?treeNum meshv:parentTreeNumber+ ?ancestorTreeNum .
#                    ?ancestor meshv:treeNumber ?ancestorTreeNum .
#                    ?ancestor rdfs:label ?alabel
#                }
#
#                """)

#                      ?d a meshv:Descriptor .
#                      ?d meshv:identifier ?mui .
#                      ?d meshv:concept ?c .
#                      FILTER(REGEX(?dName,'infection','i') || REGEX(?cName,'infection','i'))
#                      ?d rdfs:label "cancer"@en .
searchterm = """cancer"""
query ="""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
                PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
                PREFIX mesh2019: <http://id.nlm.nih.gov/mesh/2019/>
                PREFIX mesh2018: <http://id.nlm.nih.gov/mesh/2018/>
                PREFIX mesh2017: <http://id.nlm.nih.gov/mesh/2017/>

                SELECT ?d ?dname ?mui
                FROM <http://id.nlm.nih.gov/mesh>
                WHERE {
                      ?d meshv:identifier ?mui .
                      ?d meshv:concept ?c .
                      ?d rdfs:label ?dname .
                      ?c rdfs:label "Cancer"@en
                }
                ORDER BY ?d
                """











sparql.setQuery("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
                PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
                PREFIX mesh2019: <http://id.nlm.nih.gov/mesh/2019/>
                PREFIX mesh2018: <http://id.nlm.nih.gov/mesh/2018/>
                PREFIX mesh2017: <http://id.nlm.nih.gov/mesh/2017/>

                SELECT ?d ?dname ?mui
                FROM <http://id.nlm.nih.gov/mesh>
                WHERE {
                      ?d meshv:identifier ?mui .
                      ?d meshv:concept ?c .
                      ?d rdfs:label ?dname .
                      ?c rdfs:label "Cancer"@en
                }
                ORDER BY ?d
                """)


#sparql.setReturnFormat(XML)
#results = sparql.query().convert()
#print(results.toxml())

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#for result in results["results"]["bindings"]:
#    print(result["label"]["value"])
