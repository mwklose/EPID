library(ggplot2)
library(rlang)
`%>%` <- magrittr::`%>%`
pull <- dplyr::pull

dat <- read.csv(file.choose())


#### Step Ribbon ####
StatStepribbon <- ggproto(
  "StatStepribbon",
  Stat,
  compute_group = function(.,
                           data,
                           scales,
                           direction = "hv",
                           yvars = c("ymin", "ymax"),
                           ...)
  {
    direction <- match.arg(direction, c("hv", "vh"))
    data <-
      as.data.frame(data)[order(data$x),]
    n <- nrow(data)
    
    if (direction == "vh") {
      xs <- rep(1:n, each = 2)[-2 * n]
      ys <-
        c(1, rep(2:n, each = 2))
    } else {
      ys <- rep(1:n, each = 2)[-2 * n]
      xs <-
        c(1, rep(2:n, each = 2))
    }
    
    data.frame(x = data$x[xs]
               , data[ys, yvars, drop = FALSE]
               , data[xs, setdiff(names(data), c("x", yvars)), drop =
                        FALSE])
  },
  required_aes = c("x", "ymin", "ymax"),
  default_geom = GeomRibbon,
  default_aes = aes(x = ..x.., ymin = ..y.., ymax =
                      Inf)
)

stat_stepribbon = function(mapping = NULL,
                           data = NULL,
                           geom = "ribbon",
                           position = "identity") {
  layer(
    stat = StatStepribbon,
    mapping = mapping,
    data = data,
    geom = geom,
    position = position
  )
}


# This is awful: https://dplyr.tidyverse.org/articles/programming.html
# Get Bounds transforms a normally distribution 95% confidence interval into a PERCENTILE confidence interval.
get_bounds <-
  function(dat = dat,
           percentile = 0.95,
           xvar = RD,
           lcl = RD_LCL,
           ucl = RD_UCL,
           yvar = t,
           log_scale = FALSE) {
    
    myt <- {{dat}} %>% pull({{ yvar }})
    mid <- {{ dat }} %>% pull({{ xvar }})
    upper <- {{ dat }} %>% pull({{ ucl }})
    
    if(log_scale){
      diff <- (log(upper) - log(mid)) / qnorm(0.975)
      lowercl <- exp(log(mid) - qnorm(percentile) * diff)
      uppercl <- exp(log(mid) + qnorm(percentile) * diff)
    } else {
      diff <- (upper - mid) / qnorm(0.975)
      lowercl <- mid - qnorm(percentile) * diff
      uppercl <- mid + qnorm(percentile) * diff
    }
    
    
    
    d <-
      data.frame(
        yvar = myt,
        lcl = lowercl,
        xvar = mid,
        ucl = uppercl
      )
    return(d)
  }

vec_l <- lapply(vec, get_bounds, d=dat, xvar=RR, lcl=RR_LCL, ucl=RR_UCL, yvar=t, log_scale=TRUE)

sierra_plot <- function(dat,
                        xvar = RD,
                        lcl = RD_LCL,
                        ucl = RD_UCL,
                        yvar = t,
                        xlab = "Risk Difference",
                        ylab = "Days",
                        reference_line = 0.0,
                        log_scale = FALSE,
                        treat_labs = c("Vaccine", "Control"),
                        step = 0.01) {
  # Anonymous function for breaks in base
  base_breaks <- function(n = 10) {
    function(x) {
      axisTicks(log10(range(x, na.rm = TRUE)),
                log = TRUE,
                n = n)
    }
  }
  
  # Set up plot environment - get values first
  vec <- seq(from = 0.50,
             to = 1 - step,
             by = step)
  vec_lapply <-
    lapply(
      vec,
      get_bounds,
      dat = {{dat}},
      xvar = {{xvar}},
      lcl = {{lcl}},
      ucl = {{ucl}},
      log_scale = {{log_scale}}
    )
  
  t_lim <- max({{dat}} %>% pull({{yvar}}))
  
  if (log_scale) {
    x_lim <- max(abs(log({{dat}} %>% pull({{ucl}}))),
    abs(log({{dat}} %>% pull({{lcl}}))))
    
    y_scale = scale_y_continuous(
      limits = c(exp(-x_lim), exp(x_lim)),
      trans = "log",
      breaks = base_breaks()
    )
    text_loc = c(-x_lim / 2, x_lim / 2)
  } else {
    x_lim <- max(abs({{dat}} %>% pull({{lcl}})), 
                 abs({{dat}} %>% pull({{ucl}})))
    y_scale = scale_y_continuous(limits = c(-x_lim, x_lim))
    text_loc = c(-x_lim / 2, x_lim / 2)
  }
  
  
  # Actually plot
  p <- ggplot() 

  for (v in vec_lapply) {
    p <- p + geom_ribbon(
      data = v,
      aes(x=yvar, y=xvar, ymin = lcl, ymax = ucl),
      stat = "identity",
      alpha = 5 * {{step}},
      fill = "gray20"
    )
  }
  
  # Add Step Function
  p <- p + geom_step() +
    # Add Reference Line
    geom_hline(yintercept = reference_line, linetype = "dotted") +
    y_scale +
    scale_x_continuous(limits = c(0, t_lim), expand = c(0, 0)) +
    coord_flip(clip = "off") +
    theme(
      axis.line = element_line(colour = "black"),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_blank(),
      panel.border = element_rect(colour = "black", fill = NA),
      plot.margin = unit(c(2, 1, 1, 1), "lines")
    ) +
    geom_text(
      data = head({{dat}}, 1),
      label = sprintf("Favors %s", treat_labs[1]),
      x = t_lim + 5,
      y = text_loc[1]
    ) +
    geom_text(
      data = head({{dat}}, 1),
      label = sprintf("Favors %s", treat_labs[2]),
      x = t_lim + 5,
      y = text_loc[2]
    ) +
    xlab(ylab) +
    ylab(xlab)
  p
}

sierra_plot(
  dat = dat,
  xvar = RD,
  lcl = RD_LCL,
  ucl = RD_UCL,
  yvar = t,
  treat_labs = c("Vaccine", "Control")
)

sierra_plot(
  dat = dat,
  xvar = RR,
  lcl = RR_LCL,
  ucl = RR_UCL,
  yvar = t,
  treat_labs = c("Vaccine", "Control"),
  reference_line = 1.0,
  step=0.01,
  log_scale = TRUE
)
