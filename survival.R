library("survival")
library("survminer")

setwd("/mnt/c/Users/power/My\ Documents/GBM_Project/GDC_DATA/Genes")
# file_list <- list.files(path="/mnt/c/Users/power/My\ Documents/GBM_Project/GDC_DATA/Genes")
# files <- list.files(pattern = "txt")
file_list <- list.files(pattern = "\\.txt$")

for (i in 1:length(file_list)){
    print(file_list[[i]])
    data1 <- read.table(file_list[i], header=F)
    
    attach(data1)
    fit <- survfit(Surv(V2, V3) ~ V4, data = data1)
    print(fit)
    ptable <- surv_pvalue(
      fit,
      data = data1,
      method = "survdiff",
      test.for.trend = FALSE,
      combine = FALSE
    )
    pval <- ptable[[4]]
 

    pp <- ggsurvplot(fit,
           pval = TRUE, conf.int = TRUE,
           risk.table = TRUE, # Add risk table
           risk.table.col = "strata", # Change risk table color by groups
           linetype = "strata", # Change line type by groups
           surv.median.line = "hv", # Specify median survival
           ggtheme = theme_bw(), # Change ggplot2 theme
           palette = c("#E7B800", "#2E9FDF"))
    ggsave(paste(substr(pval,5,nchar(pval)),file_list[i],"plot.png",sep = "_"), print(pp))
    
    detach(data1)

}

