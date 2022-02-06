import mutational_neighborhood.generate_traps
import mutational_neighborhood.run_exp
import mutational_neighborhood.explore_single_mutation

mutational_neighborhood.generate_traps.generate_traps("random", 2)
#mutational_neighborhood.explore_single_mutation.explore_single_mutation("inputs.csv", "outputs.csv")
func, sub_df_name, output_file_name = mutational_neighborhood.run_exp.run_exp(1,'single',True)
mutational_neighborhood.explore_single_mutation.explore_single_mutation(sub_df_name, output_file_name)
