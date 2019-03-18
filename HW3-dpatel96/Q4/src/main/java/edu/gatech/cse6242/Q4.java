package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {

  public static class DiffMapper extends 
    Mapper<Object,  /*Input Key Type*/
    Text,           /*Input Value Type*/
    IntWritable,    /*Output Key Type*/
    IntWritable>    /*Output Value Type*/
    {
      
      private IntWritable nodeSource = new IntWritable();
      private IntWritable nodeTarget = new IntWritable();
      private static IntWritable inDegree = new IntWritable(-1);
      private static IntWritable outDegree = new IntWritable(1);


      public void map(Object key, Text value, Context context) 
        throws IOException, InterruptedException {
          String[] values = value.toString().split("\t");

          nodeSource.set(new Integer(values[0]));
          nodeTarget.set(new Integer(values[1]));
          
          context.write(nodeSource, outDegree);
          context.write(nodeTarget, inDegree);
      }
    }

  public static class DiffReducer extends
    Reducer<IntWritable,         /* Input Key Type */ 
    IntWritable,                 /* Input Value Type */
    IntWritable,                 /* Output Key Type */
    IntWritable>                 /* Input Value Type */
    {
    private IntWritable diff = new IntWritable();

	  public void reduce(IntWritable key, Iterable<IntWritable> values, Context context)
      throws IOException, InterruptedException {
    
      int sum = 0;
      for (IntWritable value : values) {
        sum += value.get();
      }

      diff.set(sum);
      context.write(key, diff);
      }
    }

  public static boolean getDiffMR(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");

    job.setJarByClass(Q4.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    job.setMapperClass(DiffMapper.class);
    job.setCombinerClass(DiffReducer.class);
    job.setReducerClass(DiffReducer.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1] + "_TMP"));

    return job.waitForCompletion(true);
  }

  public static class CountMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{

      private IntWritable diff = new IntWritable();
      private static IntWritable count = new IntWritable(1);

      public void map(Object key, Text value, Context context) 
        throws IOException, InterruptedException {
          String[] values = value.toString().split("\t");

          diff.set(new Integer(values[1]));
          context.write(diff, count);
      }
    }

  public static class CountReducer
      extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
      private IntWritable count = new IntWritable();

      public void reduce(IntWritable key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
          int sumCount = 0;
          for (IntWritable value : values) {
            sumCount += value.get();
          }

          count.set(sumCount);
          context.write(key, count);
        }
    }

  public static boolean getCountMR(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");

    job.setJarByClass(Q4.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    job.setMapperClass(CountMapper.class);
    job.setCombinerClass(CountReducer.class);
    job.setReducerClass(CountReducer.class);

    FileInputFormat.addInputPath(job, new Path(args[1] + "_TMP"));
    // FileInputFormat.addInputPath(job, new Path("/home/cse6242/Desktop/Q4/data/tmp.tsv"));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    return job.waitForCompletion(true);
  }

  public static void main(String[] args) throws Exception {

    boolean diffCompleted = getDiffMR(args);
    System.out.println(diffCompleted);
    if (!diffCompleted) System.exit(1);

    boolean countCompleted = getCountMR(args);
    if (!countCompleted) System.exit(1);

    System.exit(0);
  }
}
