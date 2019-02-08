package project;

import java.io.*;
import java.nio.charset.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;

import static java.nio.charset.StandardCharsets.UTF_8;
import static java.nio.file.Files.*;
import static java.nio.file.Files.newBufferedReader;
import static java.nio.file.Paths.get;


public class CS242_Index 
{
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
        while(i<2) {
            Document doc = new Document();
            try (BufferedReader r = newBufferedReader(Paths.get(file_path.concat(i.toString()).concat(".txt")),StandardCharsets.UTF_8)) {
                String line;
                while((line = r.readLine()) != null){
                        doc.add(new TextField("content", line, Field.Store.YES) );
                        //print out what is being added to the document for testing purposes
                        System.out.println("Reading Line: "+line);
                }
                i++;

            }
            indexWriter.addDocument(doc);
        }

        indexWriter.close();

        // Now search the index:
        DirectoryReader indexReader = DirectoryReader.open(directory);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        QueryParser parser = new QueryParser("content", analyzer);
        
        //This is the query that you'll be indexing the documents by
        Query query = parser.parse("ingredients");

        System.out.println("");
        System.out.println("------------------------ RESULTS --------------------------");
        System.out.println(query.toString());
        int topHitCount = 100;
        ScoreDoc[] hits = indexSearcher.search(query, topHitCount).scoreDocs;

        // Iterate through the results:
        for (int rank = 0; rank < hits.length; ++rank) {
            Document hitDoc = indexSearcher.doc(hits[rank].doc);
            System.out.println((rank + 1) + " (score:" + hits[rank].score + ")--> " + hitDoc.get("content"));
//             System.out.println(indexSearcher.explain(query, hits[rank].doc));
        }
        indexReader.close();
        directory.close();


    }
}
