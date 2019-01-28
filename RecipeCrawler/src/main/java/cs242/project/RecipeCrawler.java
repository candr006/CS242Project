package cs242.project;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;

import java.io.IOException;
import java.util.HashSet;

public class RecipeCrawler {
    private static final int MAX_DEPTH = 5;
    private HashSet<String> links;

    public RecipeCrawler() {
        links = new HashSet<String>();
    }

    public void getPageLinks(String URL, int depth) {
        if ((!links.contains(URL) && (depth < MAX_DEPTH))) {
            System.out.println(">> Depth: " + depth + " [" + URL + "]");
            try {
                links.add(URL);

                Document document = Jsoup.connect(URL).get();
                Elements linksOnPage = document.select("a[href]");
                Elements recipes = document.select("div.fd-recipe");
                for(Element recipe : recipes) {
                    System.out.println("data-url: "+recipe.attr("data-url"));
                }
                Elements recipeFacts = document.select("div.recipe-facts");
                Elements ingredientList = document.select("div.ingredient-list");
                Elements directions = document.select("div.directions");
                String bodytext = document.body().text();

                FileWriter fileWriter = new FileWriter("output_recipe.txt");
                PrintWriter printWriter = new PrintWriter(fileWriter);
                printWriter.print(bodytext);
                System.out.println("RF: " +recipeFacts.text());
                System.out.println("IL: " +ingredientList.text());
                System.out.println("DIR: " +directions.text());




                depth++;
                for (Element page : linksOnPage) {
                    getPageLinks(page.attr("abs:href"), depth);
                }
            } catch (IOException e) {
                System.err.println("For '" + URL + "': " + e.getMessage());
            }
        }
    }

    public static void main(String[] args) {
        new RecipeCrawler().getPageLinks("http://www.geniuskitchen.com/recipe", 0);
    }
}