package edu.gatech.cse6242;

import java.io.IOException;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {

  public static class EmailMapper
    extends Mapper<Object, Text, Text, IntWritable>{
      private static IntWritable count;
      private Text person = new Text();

      public void map(Object key, Text value, Context context) 
        throws IOException, InterruptedException {
          String[] values = value.toString().split("\t");

          person.set(values[1]);
          count = new IntWritable(Integer.parseInt(values[2]));
          context.write(person, count);
      }
    }

    public static class EmailReducer
      extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context)
          throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
              sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
          }
      }




  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */
    job.setJarByClass(Q1.class);
    job.setMapperClass(EmailMapper.class);
    job.setCombinerClass(EmailReducer.class);
    job.setReducerClass(EmailReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
