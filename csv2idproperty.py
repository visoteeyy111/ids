import csv
import html

def convert_csv_to_id_properties(csv_file_path, ontology_uri_base, output_file):
    with open(csv_file_path, newline='', encoding='cp1252') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:

        reader = csv.DictReader(csvfile, delimiter="\t")

        outfile.write(
            '<?xml version="1.0"?>\n'
            '<rdf:RDF\n'
            '    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
            '    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
            '    xmlns:owl="http://www.w3.org/2002/07/owl#"\n'
            '    xmlns:obo="http://www.geneontology.org/formats/oboInOwl#"\n'
            '    xmlns:vitro="http://vitro.mannlib.cornell.edu/ns/vitro/public#">\n\n'
        )

        for row_num, row in enumerate(reader, start=2):
            if row.get("include (y/n/?)", "").strip().lower() != "y":
                continue

            property_id = (row.get("property_name") or "").strip()
            if not property_id:
                continue

            def esc(v):
                return html.escape(v.strip())

            outfile.write(f"""

    <!-- {ontology_uri_base}#{property_id} -->

    <owl:DatatypeProperty rdf:about="{ontology_uri_base}#{property_id}">
""")

            # Labels
            if row.get("label"):
                outfile.write(
                    f'        <rdfs:label xml:lang="en">{esc(row["label"])}</rdfs:label>\n'
                )

            if row.get("preferred_label"):
                outfile.write(
                    f'        <obo:IAO_0000111 xml:lang="en">{esc(row["preferred_label"])}</obo:IAO_0000111>\n'
                )

            if row.get("alt_label"):
                outfile.write(
                    f'        <obo:IAO_0000118 xml:lang="en">{esc(row["alt_label"])}</obo:IAO_0000118>\n'
                )

            # Descriptive annotations
            if row.get("comment"):
                outfile.write(
                    f'        <rdfs:comment xml:lang="en">{esc(row["comment"])}</rdfs:comment>\n'
                )

            if row.get("example"):
                example = esc(row["example"])
                outfile.write(
                    f'        <obo:IAO_0000112>{example}</obo:IAO_0000112>\n'
                )
                outfile.write(
                    f'        <vitro:exampleAnnot>{example}</vitro:exampleAnnot>\n'
                )

            if row.get("formal_definition"):
                outfile.write(
                    f'        <obo:IAO_0000115>{esc(row["formal_definition"])}</obo:IAO_0000115>\n'
                )

            if row.get("definition_source"):
                outfile.write(
                    f'        <obo:IAO_0000119>{esc(row["definition_source"])}</obo:IAO_0000119>\n'
                )

            # Domains
            for domain_key in ("domain 1", "domain 2"):
                domain = row.get(domain_key, "").strip()
                if domain:
                    outfile.write(
                        f'        <rdfs:domain rdf:resource="{domain}"/>\n'
                    )

            # Superproperty
            outfile.write(
                '        <rdfs:subPropertyOf rdf:resource="http://vivoweb.org/ontology/core#identifier"/>\n'
                '    </owl:DatatypeProperty>\n'
            )

        outfile.write('\n</rdf:RDF>\n')


# Run
convert_csv_to_id_properties(
    "id_properties.csv",
    "http://example.org/ontology/core",
    "new_properties.owl"
)