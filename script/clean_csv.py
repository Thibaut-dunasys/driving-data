# Nettoayge des CSV Speed, EngineSpeed, Odometer, 

df clean_odometer(df_odo):

  # df_odo= pd.read_csv(path_distanceTotalizer)
  df_odo = df_odo.rename(columns={"capability": "DistanceTotalizer(km)"})
  # dfodo["Time"] = pd.to_datetime(dfodo["Time"])
  df_odo['DistanceTotalizer(km)'] = (
      df_odo['DistanceTotalizer(km)']
      .astype(str)             
      .str.replace('rpm', '', regex=False)  
      .str.strip()             
      .astype(float)           
      .astype(int)             
  )
 return df_odo
