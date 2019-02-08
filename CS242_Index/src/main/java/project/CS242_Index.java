package project;

import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.IOException;

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

        String[] pages = {
                "Search engine is considered the most successful application of IR.",
                "Collect your data and index with Lucene",
                "index your data using Hadoop and build Web Interface",
        };
        for (String page: pages) {
            Document doc = new Document();
            doc.add(new TextField("content", page, Field.Store.YES));
            indexWriter.addDocument(doc);
        }
        indexWriter.close();

        // Now search the index:
        DirectoryReader indexReader = DirectoryReader.open(directory);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        QueryParser parser = new QueryParser("content", analyzer);
        Query query = parser.parse("index data");

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
