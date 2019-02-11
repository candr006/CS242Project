package project;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexableField;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.jsoup.Jsoup;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.Callable;

import static java.nio.file.Files.newBufferedReader;





public class CS242_Index 
{
    public static String remove_html(String html) {
        if(html != null && !html.isEmpty()) {
            String text = Jsoup.parse(html).text();
            return text;
        }
        else return "";
    }

    public static void main( String[] args ) throws IOException, ParseException {
        Analyzer analyzer = new StandardAnalyzer();

        // Store the index in memory:
        Directory directory = new RAMDirectory();
        // To store an index on disk, use this instead:
        //Directory directory = FSDirectory.open("/tmp/test");
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter indexWriter = new IndexWriter(directory, config);


        //this is where the outputs of the crawler are stored
        //iterate through all the crawled files
        String file_path="outputs/foodie_crush_output";
        Integer i=1;
        while(i<32) {
            if(i!=26) {
                System.out.println("Page: " + i);
                Document doc = new Document();
                try (BufferedReader r = newBufferedReader(Paths.get(file_path.concat(i.toString()).concat(".txt")), StandardCharsets.UTF_8)) {
                    String line;
                    String cleanLine;
                    String field_name;
                    while ((line = r.readLine()) != null) {
                        field_name="content";
                        if(line.contains("<meta property=\"og:url\" content=\"")){
                            String[] url_parts=line.split("<meta property=\"og:url\" content=\"");
                            String url =url_parts[1].substring(0, url_parts[1].length() - 4);
                            doc.add(new TextField("url", url, Field.Store.YES));
                        }
                        cleanLine = remove_html(line);

                        if (!cleanLine.isEmpty()) {
                            //I put stars in the crawler output to separate the recipes
                            if (cleanLine.equals("*********************************************************")) {
                                //when the line being read is stars (recipe separator), add the doc to the index and create a new doc
                                indexWriter.addDocument(doc);
                                doc = new Document();

                            } else {
                                doc.add(new TextField(field_name, cleanLine, Field.Store.YES));
                                //print out what is being added to the document for testing purposes
                                //System.out.println("Reading Line: " + cleanLine);
                            }
                        }
                    }

                }


                }
            i++;
        }

        indexWriter.close();

        // Now search the index:
        DirectoryReader indexReader = DirectoryReader.open(directory);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        QueryParser parser = new QueryParser("content", analyzer);

        //This is the query that you'll be indexing the documents by
        Query query = parser.parse("turkey");

        System.out.println("");
        System.out.println("------------------------ RESULTS --------------------------");
        System.out.println(query.toString());
        int topHitCount = 100;
        ScoreDoc[] hits = indexSearcher.search(query, topHitCount).scoreDocs;

        // Iterate through the results:
        for (int rank = 0; rank < hits.length; ++rank) {
            Document hitDoc = indexSearcher.doc(hits[rank].doc);
            System.out.println((rank + 1) + " (score:" + hits[rank].score + ")--> " + hitDoc.get("content")+" -- "+hitDoc.get("url"));

        }
        indexReader.close();
        directory.close();


    }
}
