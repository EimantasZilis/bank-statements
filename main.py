import data
import plot
import stats
    
df = data.initialise()
data.write_csv(df)
plot.all(df)
