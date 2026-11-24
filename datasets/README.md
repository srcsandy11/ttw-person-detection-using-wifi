# Datasets

| Folder | Contents |
| --- | --- |
| [public](public/) | Third-party measurements. Each included sample has its own provenance and scope. |
| [custom](custom/) | Measurements collected by the project team. The [classroom index](custom/classroom-csi/index.csv) lists trials and paths relative to the index. |
| [synthetic](synthetic/) | Generated fixtures for development and replay. |

Use the [dataset registry](dataset_registry.csv) for acquisition sources, including larger research datasets hosted upstream. An upstream URL identifies the source. Browse the public folder to see which measurements ship in this checkout.

When adding a dataset, record its source, version, labels, units and redistribution terms. Preserve original session IDs. Separate room activity from corridor activity and keep all windows from a recording together when making train/test splits. Recordings from different hardware can require different feature extractors. Use independent real recordings to evaluate hardware performance.
