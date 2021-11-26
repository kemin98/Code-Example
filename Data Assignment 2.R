library(tidyverse)
library(ggplot2)

#Problem 1 
setwd("C:/Users/Kemin/Desktop/Grad/2021 Spring/Energy in the Developing World/HW 2")

village_data <- read.csv('village_surveys.csv')

view(village_data)

#(1)

#group the data
avg_energy_share_by_source <- village_data %>% 
  group_by(technology) %>% 
  summarise(avg_eshare = mean(marketshare))

view(avg_energy_share_by_source)

#plot
ggplot(data=avg_energy_share_by_source, 
       aes(x=technology, y=avg_eshare))+
  geom_bar(stat="identity", fill="steelblue")+
  ggtitle('Energy Share by Source')+
  ylab('average energy share')

#(2)

#plot for price
ggplot(data=village_data,aes(x=price))+
  geom_histogram(color="darkblue", fill="lightblue")+
  ggtitle('Price Distribution')

#plot for hours
ggplot(data=village_data,aes(x=peakhours))+
  geom_histogram(color="darkblue", fill="lightblue")+
  ggtitle('Peak Hours of Power Provided Distribution')+
  xlab('hours provided')

#plot for load
ggplot(data=village_data,aes(x=load))+
  geom_histogram(color="darkblue", fill="lightblue")+
  ggtitle('Electrical Load Distribution')

#check for mean 
summary(village_data)

#check for standard deviation.

apply(village_data,2,sd)

#(3)

#Run a regression

reg_market_share <- lm(marketshare~load+price+peakhours,
                       data=village_data)

summary(reg_market_share)

#(4)

#Create two new binary variables called campaign and China. Campaign
#will equal to 1 for all grid and 0 for others.Similarly, China 
#would equal to 1 for all ownsolar and 0 for others.

village_data <- village_data %>% mutate(
  campaign=if_else(technology=='grid',1,0),
  China=if_else(technology=='ownsolar',1,0)
)

#run a regression with two additional variables
reg_market_share_add <- 
  lm(marketshare~load+price+peakhours+campaign+
       China,data=village_data)

summary(reg_market_share_add)

#problem 2

#(2)
appliance_data <- load('appliances.Rdata')

ggplot(data = brazil4, aes(x=percentile2, y=refrigerator))+
  geom_point()+
  geom_smooth()+
  ggtitle('Refrigerator Ownership vs. Expenditure Percentile')+
  xlab('expenditure percentile')+
  ylab('refrigerator ownership')

  

  



