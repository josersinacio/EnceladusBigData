codigos_causa_eletrica <- c("W85", "W86", "W87", "X33")
codigos_causa_clr_e_term <- c(
  "W35", "W36", "W38", "W39", "W40", "W92", "X00", "X01", "X02",
  "X03", "X04", "X05", "X06", "X08", "X09", "X10", "X11", "X12",
  "X13", "X14", "X15", "X16", "X17", "X18", "X19", "X30", "X75",
  "X76", "X77", "X88", "X96", "X97", "X98", "Y25", "Y26", "Y27"
)
codigos_causa_quimica <- c("X86")
codigos_causa_gelad_e_rad <- c(
  "W88", "W89", "W90", "W91", "W93", "X31", "X32"
)

codigos_cid10 <- c(
  # Elétrica
  codigos_causa_eletrica,
  # Calor e Térmica
  codigos_causa_clr_e_term,
  # Química
  codigos_causa_quimica,
  # Outros (geladura, radiação)
  codigos_causa_gelad_e_rad
)
