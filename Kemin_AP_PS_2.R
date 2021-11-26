#AP Q3

#install sf

install.packages("sf")
install.packages("rnaturalearth")
install.packages("rnaturalearthdata")
install.packages("rgeos")
#Load packages

library(tidyverse)
library(sf)
library(ggplot2)
library("rnaturalearth")
library("rnaturalearthdata")
library("rgeos")

#set working directory

setwd("C:/Users/Kemin/Desktop/Grad/2021 Winter/AP/PS/2")

#load the world sf data

world <- ne_countries(scale = "medium", returnclass = "sf")


#load the IAEP data

country_data_labels <- read.csv("IAEPv2_0_2015labels.csv")

#filter the observations from 2011 in IAEP dataset

country_data_labels_2011 <- country_data_labels %>% 
  filter(year==2011)


#left join the IAEP and the world dataset

whole_world <- merge(country_data_labels_2011,world,
                     by.x=c("cname"),by.y=c("admin"),
                      all.y = TRUE)


View(whole_world)

#check lelecsystem

unique(whole_world$lelecsystem)


# code N/A and Missing information all as "Missing"
whole_world <- whole_world %>% 
  mutate(lelecsystem=
           case_when(lelecsystem==
                       "N/A - no elected legislature"~"Missing",
            lelecsystem=="Missing information"~"Missing",
            is.na(lelecsystem)~"Missing",
            TRUE~lelecsystem))


#create a map showing the electoral systems across the world

ggplot(data=whole_world)+
  geom_sf(aes(geometry=geometry,fill=lelecsystem))+
  ggtitle("Electoral Systems across the World",
          subtitle = paste0("(",length(whole_world$cabr),
                            " countries)"))+xlab("Longitude") + 
  ylab("Latitude") + 
  labs(fill="Electoral System",
                          caption = "Missing include N/A - no elected legislature and Missing information")



#(b)

#drop observations with missing information in number of 
#effective parties for clear comparison

whole_world_parties <- whole_world %>% 
  filter(!parties=="Missing information")

#make a bar plot 
ggplot(data = whole_world_parties)+geom_bar(
  aes(x=parties,fill=lelecsystem,alpha=0.8)
)+ggtitle("Number of Effective Parties within Diffrent Electoral Systems ",
          subtitle = paste0("(",length(whole_world_parties$parties)," countries)"))+
  labs(fill="Electoral System")


unique(whole_world$parties)

#(c)There are two redundant lines explaining the 
#source of data at the top of the csv file that prevent
#R read the csv. So we first removed those two lines ourselves 
#in that csv.

world_bank_data <- read.csv("World_Bank_data.csv")


View(world_bank_data)

#calculate average government spending from 2000 to 2012

world_bank_data <- world_bank_data %>% 
  mutate(avg_spending=select(.,X2000:X2012) %>% rowMeans
         (na.rm = TRUE) )

world_bank_data <- world_bank_data1 %>% select(
  ï..Country.Name,avg_spending
)

#merge whole_world and world_bank_data

whole_world_spending <- merge(whole_world,world_bank_data,
                     by.x=c("cname"),by.y=c("ï..Country.Name"),
                     all.x = TRUE)


View(whole_world_spending)

#draw a density plot showing the relationship

ggplot(data = whole_world_spending)+geom_density(
  aes(x=avg_spending,fill=lelecsystem,alpha=0.8)
)+ggtitle("Average Government spending as a % of GDP under Different Electoral Systems ",
          subtitle = paste0("(",length(whole_world_spending$lelecsystem)," countries)"))+
  labs(fill="Electoral System",caption = 
         "Missing include N/A - no elected legislature and Missing information")+
  xlab("Average Government Spending as a % of GDP from 2000 to 2012")




