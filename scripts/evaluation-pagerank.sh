# ask input, case name
# 1. Run name extract ( ask input )
# 2. Grep file to with ###
# 3. Run pagerank
# 4. Copy pagerank to namegraph/

case_name=$1
grouping=$2

temp_graph="raw_$case_name"
output_graph="name-graph/$case_name"
pagerank_output="name-graph/rank-$case_name"

rm -rf "output-pagerank"

echo "Evaluating case '$case_name' with $grouping sentences"

echo "Extracting name from documents" \
&& python scripts/name-graph-pagerank.py $grouping > $temp_graph \
&& cat $temp_graph | grep '###' | awk '{ print $2,$3 }' > "$output_graph" \
&& echo "Calculating pagerank" \
&& /usr/local/Cellar/apache-spark/1.3.1_1/bin/spark-submit pagerank.py "$output_graph" 0.9 && head "output-pagerank/part-00000" \
&& mv "output-pagerank/part-00000" $pagerank_output \
&& echo "Generating ./web/$case_name.json" \
&& python scripts/json-name-flare-graph.py $output_graph $pagerank_output  > "web/flare-$case_name.json" 
