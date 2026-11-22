package assignment;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import java.time.Duration;
import java.util.Random;

public class PatientStream {
  public static class Vital implements java.io.Serializable {
    public String patient; public long timestamp; public int heartRate; public double temperature;
    public Vital() {} public Vital(String p,long t,int h,double temp){patient=p;timestamp=t;heartRate=h;temperature=temp;}
    public String toString(){return patient+" ts="+timestamp+" heart="+heartRate+" temperature="+temperature;}
  }
  public static class Sensor implements SourceFunction<Vital> {
    private volatile boolean running=true;
    public void run(SourceContext<Vital> ctx) throws Exception {
      Random r=new Random(42); long base=1735689600000L;
      for(int i=0;i<60 && running;i++) { synchronized(ctx.getCheckpointLock()) {ctx.collect(new Vital("P"+(i%3+1),base+i*1000L,60+r.nextInt(81),Math.round((36+r.nextDouble()*4)*10)/10.0));} Thread.sleep(100); }
    }
    public void cancel(){running=false;}
  }
  public static class Summary extends ProcessWindowFunction<Vital,String,String,TimeWindow> {
    public void process(String key, Context context, Iterable<Vital> values, Collector<String> out){int n=0,sum=0;double temp=0;for(Vital v:values){n++;sum+=v.heartRate;temp+=v.temperature;}out.collect(String.format(java.util.Locale.ROOT,"SUMMARY patient=%s window=[%d,%d) count=%d mean_heart=%.1f mean_temp=%.1f",key,context.window().getStart(),context.window().getEnd(),n,(double)sum/n,temp/n));}
  }
  public static void main(String[] args) throws Exception {
    StreamExecutionEnvironment env=StreamExecutionEnvironment.getExecutionEnvironment(); env.setParallelism(1);
    var vitals=env.addSource(new Sensor()).assignTimestampsAndWatermarks(WatermarkStrategy.<Vital>forBoundedOutOfOrderness(Duration.ofSeconds(1)).withTimestampAssigner((v,t)->v.timestamp));
    vitals.filter(v->v.heartRate>120 || v.temperature>=38.0).map(v->"ALERT "+v).print();
    vitals.keyBy(v->v.patient).window(TumblingEventTimeWindows.of(Time.seconds(10))).process(new Summary()).print();
    env.execute("Synthetic patient vitals");
  }
}
