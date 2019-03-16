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

  public static class DiffMapper
    extends Mapper<Object, Text, IntWritable, Text>{
      
      private IntWritable nodeSource = new IntWritable();
      private IntWritable nodeTarget = new IntWritable();
      private static Text indegree = new Text("1\t0");
      private static Text outdegree = new Text("0\t1");

      public void map(Object key, Text value, Context context) 
        throws IOException, InterruptedException {
          String[] values = value.toString().split("\t");

          nodeSource.set(values[0]);
          nodeTarget.set(values[1]);
          
          context.write(nodeSource, indegree);
          context.write(nodeTarget, outDegree);
      }
    }

  public static class DiffReducer
      extends Reducer<IntWritable, Text, IntWritable, Text> {
        private IntWritable inDegree;
        private IntWritable outDegree;
        private Text result;

        public void reduce(IntWritable key, Iterable<Text> values, Context context)
          throws IOException, InterruptedException {
            int sumIn = 0;
            int sumOut = 0;
            for (Text value : values) {
              String[] degrees = value.get().toString().split("\t");
              
              sumIn += degrees[0];
              sumOut += degrees[1];
            }
            int diff = sumOut - sumIn;

            result.set(sumIn + "\t" + sumOut + "\t" + diff);
            context.write(key, result);
          }
      }

  public static int getDiffMR(String[] args) {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");

    job.setJarByClass(Q4.class);
    job.setMapperClass(GraphMapper.class);
    job.setCombinerClass(GraphReducer.class);
    job.setReducerClass(GraphReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("TMP_" + args[1]));

    return job.waitForCompletion(true)
  }

  public static class CountMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{

      private IntWritable diff = new IntWritable();
      private static IntWritable count = new IntWritable(1)

      public void map(Object key, Text value, Context context) 
        throws IOException, InterruptedException {
          String[] values = value.toString().split("\t");

          diff.set(values[3]);
          context.write(diff, count);
      }
    }

  public static class CountReducer
      extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
        private IntWritable result;

        public void reduce(IntWritable key, Iterable<Text> values, Context context)
          throws IOException, InterruptedException {
            int sumCount = 0;
            for (Text value : values) {
              sumCount += value.get();
            }

            result.set(sumCount);
            context.write(key, result);
          }
      }

  public static int getCountMR(String[] args) {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");

    job.setJarByClass(Q4.class);
    job.setMapperClass(CountMapper.class);
    job.setCombinerClass(CountReducer.class);
    job.setReducerClass(CountReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path("TMP_" + args[1]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    return job.waitForCompletion(true)
  }

  public static void main(String[] args) throws Exception {

    diffCompleted = getDiffMR(args);
    if (~diffCompleted) System.exit(1);

    countCompleted = getCountMR(args);
    if (~countCompleted) System.exit(1);

    System.exit(0);
  }
}
