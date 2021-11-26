#Kemin Wang AP HW3

#Load packages

library(tidyverse)
library(ggplot2)


#set working directory

setwd("C:/Users/Kemin/Desktop/Grad/2021 Winter/AP/PS/3")

#load the data

Chile_data <- read.csv("Turnout_Chile.csv")

View(Chile_data)

#(a)

avg_voter_turnout_by_age <- Chile_data %>% group_by(
  age
) %>% summarise(
  avg_voter_turnout=mean(voted)
)

View(avg_voter_turnout_by_age)


#create a barplot

ggplot(data = avg_voter_turnout_by_age,
       aes(x=age,y=avg_voter_turnout))+
  geom_bar(stat = "identity",fill="steelblue",alpha=0.8)+ggtitle(
    "Average Voter Turnout Rate by Age in 2017"
  )+xlab("Age")+ylab("Average Voter Turnout Rate")+
  scale_x_continuous(breaks = pretty(avg_voter_turnout_by_age
                                     $age, n = 10))

#(c)

#create a table

avg_voter_turnout_by_region <- Chile_data %>% group_by(
  region
) %>% summarise(
  avg_voter_turnout=mean(voted)
)

View(avg_voter_turnout_by_region)

#(f)

#create a new table further subseted by round

avg_voter_turnout_by_age_by_round <- Chile_data %>% group_by(
  age,runoff
) %>% summarise(
  avg_voter_turnout=mean(voted)
)

View(avg_voter_turnout_by_age_by_round)

#Create a grouped barplot

ggplot(data = avg_voter_turnout_by_age_by_round,
       aes(x=age,y=avg_voter_turnout))+
  geom_bar(stat = "identity",position = "dodge",
           alpha=0.4,aes(fill=runoff))+ggtitle(
    "Average Voter Turnout Rate by Age and Round in 2017"
  )+xlab("Age")+ylab("Average Voter Turnout Rate")+
  scale_x_continuous(breaks = pretty(avg_voter_turnout_by_age_by_round
                                     $age, n = 10))
#(h)

#create a table subsetted by gender

avg_voter_turnout_by_gender <- Chile_data %>% group_by(
  age,female
) %>% summarise(
  avg_voter_turnout=mean(voted)
) %>% mutate(
  Gender=if_else(
    female==1,"Female","Male"
  )
)

View(avg_voter_turnout_by_gender)

#Create a grouped barplot by gender

ggplot(data = avg_voter_turnout_by_gender,
       aes(x=age,y=avg_voter_turnout))+
  geom_bar(stat = "identity",position = "dodge",
           alpha=0.4,aes(fill=Gender))+ggtitle(
             "Average Voter Turnout Rate by Age by Gender in 2017"
           )+xlab("Age")+ylab("Average Voter Turnout Rate")

#(i)

#Compute years passed by after 1988

t <- 2017-1988

#Create a variable called age in 1988

Chile_data <- Chile_data %>% mutate(
  age_in_1988=age-t
)

View(Chile_data)

#Restrict the sample to individuals with ages between 10 and 25

Chile_data_1988 <- Chile_data %>% 
  filter(
    age_in_1988>9&age_in_1988<26
  )


unique(Chile_data_1988$age_in_1988)


#Create a table showing average voter turnout against age in 1988
avg_voter_turnout_against_age_in_1988 <- Chile_data_1988 %>% 
  group_by(age_in_1988) %>% summarise(
  avg_voter_turnout=mean(voted)
)

View(avg_voter_turnout_against_age_in_1988)

#Create a scatterplot of average voter turnout in 2017 against age
#in 1988


ggplot(data = avg_voter_turnout_against_age_in_1988,
       aes(x=age_in_1988,y=avg_voter_turnout))+
  geom_point()+
  geom_smooth(data = filter(avg_voter_turnout_against_age_in_1988,
                            age_in_1988>17),method="lm")+
  geom_vline(xintercept = 18)+
  geom_smooth(data = filter(avg_voter_turnout_against_age_in_1988,
                  age_in_1988<19),method = "lm")+
  xlab("Age")+
  ylab("Average Voter Turnout Rate")+
  ggtitle("Average Voter Turnout Rate in 2017 against Age in 1998")+
  scale_x_continuous(breaks = pretty(
    avg_voter_turnout_against_age_in_1988$age_in_1988,
    n=14))

#(j)


#first restrict our sample to only the first round election

Chile_data_first_round <- Chile_data %>% 
  filter(runoff==0)
View(Chile_data_first_round)

#Select the variables we need into a smaller table

avg_voter_turnout_first_round_volun_or_not <- 
  Chile_data_first_round %>% 
  select(voted,voluntary_registration) %>%
  group_by(voluntary_registration) %>% summarise(
    avg_voter_turnout=mean(voted)
  ) %>% mutate(
    v_or_not=if_else(
      voluntary_registration==1,"Voluntarily registered",
      "Automatically registered"
    )
  )

#Create a grouped barplot capturing average voter turnout in 2017 
#between voluntary registered voters and automatic registered
#voters


ggplot(data = avg_voter_turnout_first_round_volun_or_not,
       aes(x=v_or_not,y=avg_voter_turnout))+
  geom_bar(stat = "identity",position = "dodge",
           alpha=0.4,aes(fill=v_or_not))+ggtitle(
             "Average Voter Turnout Rate in 2017 between 
             Automatically Registered and Voluntarily Registered"
           )+xlab("Registration Method")+
  ylab("Average Voter Turnout Rate")+
  labs(fill="Registration Method")



View(avg_voter_turnout_first_round_volun_or_not)


#Create a new table for OLS regression of voted on 
#voluntary_registration controlling for age and female

avg_voter_turnout_first_round_OLS <- Chile_data_first_round %>% 
  select(age,voluntary_registration,voted,female) 

View(avg_voter_turnout_first_round_OLS)

#Regress voted on age,voluntary_registration and female

final_OLS <- lm(voted~age+voluntary_registration+female,
   data = avg_voter_turnout_first_round_OLS)

summary(final_OLS)




  





